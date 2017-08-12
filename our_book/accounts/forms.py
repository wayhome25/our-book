from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from django_messages.forms import ComposeForm
from django_messages.models import Message
if "pinax.notifications" in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
    from pinax.notifications import models as notification
else:
    notification = None

from .tasks import send_email_message_notification

User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'nickname', 'team', 'avatar')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'test@gmail.com',
                'required': 'True',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'test2017',
                'required': 'True',
            }
        )
    )

class NewComposeForm(ComposeForm):
    recipient = forms.ModelChoiceField(label='받는사람', queryset=User.objects.all(),
                                       widget=forms.Select({'class': 'form-control'}))
    subject = forms.CharField(label='제목', max_length=140, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label='내용',
                           widget=forms.Textarea(attrs={'rows': '12', 'cols': '55', 'class': 'form-control'}))

    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []
        msg = Message(
            sender=sender,
            recipient=recipients,
            subject=subject,
            body=body,
        )
        if parent_msg is not None:
            msg.parent_msg = parent_msg
            parent_msg.replied_at = timezone.now()
            parent_msg.save()
        msg.save()
        message_list.append(msg)

        mail_subject = '{}님이 쪽지를 보냈습니다'.format(sender.nickname)
        mail_content = '{}님의 쪽지 : {}'.format(sender.nickname, body)
        # send_mail(mail_subject, mail_content, 'wayhome250@gmail.com', [recipients.email])
        send_email_message_notification.delay(mail_subject, mail_content, user_pk=recipients.pk)

        if notification:
            if parent_msg is not None:
                notification.send([sender], "messages_replied", {'message': msg,})
                notification.send([r], "messages_reply_received", {'message': msg,})
            else:
                notification.send([sender], "messages_sent", {'message': msg,})
                notification.send([r], "messages_received", {'message': msg,})
        return message_list
