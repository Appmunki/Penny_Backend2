import re


class DebugLoggingClient:
    def __init__(self, logger=None):
        self.set_logger(logger)

    def set_logger(self, logger):
        self.logger = logger

    def augment_metadata(self, metadata, message, exception):
        if exception:
            if not metadata:
                metadata = {}
            if exception.message:
                metadata['additional_message'] = message
            if hasattr(exception, 'stripe_id') and exception.stripe_id:
                metadata['stripe_id'] = exception.stripe_id
            if hasattr(exception, 'process_state') and exception.process_state:
                metadata['process_state'] = exception.process_state
            return metadata
        else:
            return None

    def get_metadata_str(self, metadata):
        if metadata:
            fields = []
            for key in metadata:
                if isinstance(metadata[key], basestring):
                    val = re.sub('["\']', '\\\'', metadata[key])
                    if ' ' in val:
                        val = '"{}"'.format(val)
                    fields.append('{}={}'.format(key, val))
            return ' '.join(fields)
        else:
            return ''

    def log_error(self, message, exception=None, metadata=None):
        try:
            if self.logger:
                metadata = self.augment_metadata(metadata, message, exception)
                metadata_str = self.get_metadata_str(metadata)
                self.logger.info('%s - %s' % (metadata_str, message))
        except Exception as e:
            self.error('logging failed: {}'.format(e.message))

    def info(self, message):
        if self.logger:
            self.logger.info(message)

    def error(self, message):
        if self.logger:
            self.logger.error(message)

    def warning(self, message):
        if self.logger:
            self.logger.warning(message)

    def critical(self, message):
        if self.logger:
            self.logger.critical(message)

    def debug(self, message):
        if self.logger:
            self.logger.debug(message)
