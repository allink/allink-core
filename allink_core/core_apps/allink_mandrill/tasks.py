try:
    from celery import shared_task

    @shared_task
    def send_transactional_mail_celery(template_name, message, template_content):
        """
        task for Mandrill Base class to enable full async sending of messages
        """
        import mandrill
        from .config import MandrillConfig
        config = MandrillConfig()
        mandrill_client = mandrill.Mandrill(config.apikey)
        result = mandrill_client.messages.send_template(template_name=template_name,
                                                        template_content=template_content, message=message,
                                                        async=False)
        return result[0].get('status'), result[0].get('reject_reason')
except ImportError:
    pass  # If celery is not there we can't send it with it...
