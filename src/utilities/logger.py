
import logging
import time


class Log():

    def __init__(self, current_path, start_time):
    
        self.start_time = start_time
        self.current_path = current_path
        table_name = current_path.split('/')[-1].split('.py')[0]
        etl_type = current_path.split('/')[-2]
        log_path = current_path.rsplit('/', 1)[0] + '/log' + '/' + etl_type + '.log'
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        self.file_handler = logging.FileHandler(f'{log_path}')
        self.logger.addHandler(self.file_handler)
    
    def log_error(self, e, row_count=None, batch_no=None):
        run_time = time.time() - self.start_time
        formatter = logging.Formatter(f'%(asctime)s,{run_time},{self.current_path},%(levelname)s,%(message)s,{row_count},{batch_no}', '%Y-%m-%d %H:%M:%S')
        self.file_handler.setFormatter(formatter)
        
        self.logger.error(e)
        self.file_handler.close()
        self.logger.removeHandler(self.file_handler)
    
    
    def log_success(self, row_count=None, batch_no=None, keyword=None):
        run_time = time.time() - self.start_time
        formatter = logging.Formatter(f'%(asctime)s,{run_time},{self.current_path},%(levelname)s,%(message)s,{row_count},{batch_no}', '%Y-%m-%d %H:%M:%S')
        self.file_handler.setFormatter(formatter)
       
        self.logger.info(keyword)
        self.file_handler.close()
        self.logger.removeHandler(self.file_handler)



