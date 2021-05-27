import logging as info


# set up  info logging to file - see previous section for more details
info.basicConfig(level=info.DEBUG,
                 format='%(asctime)s %(name)-12s %(levelname)-8s %(lineno)d %(message)s',
                 datefmt='%m-%d %H:%M',
                 filename='loggers/logger.log',
                 filemode='a')
# define a Handler which writes INFO messages or higher to the sys.stderr

console = info.StreamHandler()
console.setLevel(info.INFO)
# set a format which is simpler for console use
formatter = info.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
info.getLogger('').addHandler(console)


class Logger():
    # def __init__():
    #     pass
        

    def create_success_log(module: str, log: str) -> None:
        '''
        create success log from this method
        '''
        try:
            success_log = info.getLogger(module)
            success_log.info(log)
        except Exception as e:
            print(e)
            # create_error_log('logger_module', str(e))

    def create_error_log(module: str, log: str):
        '''
        create error log from this method
        '''
        try:
            error_log = info.getLogger(module)
            error_log.error(log)
        except Exception as e:
            print(e)

    def create_warning_log(module: str, log: str) -> None:
        '''
        create warning log from this method
        '''
        try:
            warning_log = info.getLogger(module)
            warning_log.warning(log)
        except Exception as e:
            print(e)
            # create_error_log('logger_module', str(e))

    def create_info_log(module: str, log: str) -> None:
        '''
        create info log file from this method
        '''
        try:
            info_log = info.getLogger(module)
            info_log.info(log)
        except Exception as e:
            print(e)
            # create_error_log('logger_module', str(e))
