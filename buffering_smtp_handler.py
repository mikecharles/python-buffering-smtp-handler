import logging, logging.handlers


class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    def __init__(self, mailhost, fromaddr, toaddrs, subject, capacity,
                 logging_format):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.mailhost = mailhost
        self.mailport = None
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.formatter = logging_format
        self.setFormatter(logging.Formatter(logging_format))

    def flush(self):
        if len(self.buffer) > 0:
            try:
                import smtplib
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP(self.mailhost, port)
                if isinstance(self.toaddrs, list):  # If to addrs is a list, then join them as a string
                    toaddrs = ','.join(self.toaddrs)
                else:
                    toaddrs = self.toaddrs
                msg = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n".format(self.fromaddr, toaddrs,
                                                                         self.subject)
                for record in self.buffer:
                    s = self.format(record)
                    msg = msg + s + "\r\n"
                smtp.sendmail(self.fromaddr, self.toaddrs, msg)
                smtp.quit()
            except:
                self.handleError(None)  # no particular record
            self.buffer = []
