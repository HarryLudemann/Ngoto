from hazzah import modules
import logging


class osint:
    __version__ = '0.0.3'
    VIRUS_TOTAL_API_KEY = ''
    IP_QUALITY_API_KEY = ''
    NUM_VERIFY_API_KEY = ''

    # api key setters
    def set_virus_total_api(self, api_key):
        self.VIRUS_TOTAL_API_KEY = api_key
    def set_ip_quality_api(self, api_key):
        self.IP_QUALITY_API_KEY = api_key
    def set_num_verify_api(self, api_key):
        self.NUM_VERIFY_API_KEY = api_key

    # getters
    def get_ip_info(self, target_ip):
        if not self.IP_QUALITY_API_KEY:
            logging.error('IP Quality API key not set')
            return {}
        else:
            return modules.get_ip_info(target_ip, self.IP_QUALITY_API_KEY)

    def get_phone_info(self, target_phone):
        if not self.NUM_VERIFY_API_KEY:
            logging.error('Num Verify API key not set')
            return {}
        return modules.get_phone_info(target_phone, self.NUM_VERIFY_API_KEY)

    def get_email_info(self, target_email):
        return modules.get_email_info(target_email)

    def get_url_info(self, target_url):
        return modules.get_urls_info(target_url)

    def get_url_scan(self, target_url):
        if not self.VIRUS_TOTAL_API_KEY:
            logging.error('VirusTotal API key not set')
        return modules.get_url_scan(target_url, self.VIRUS_TOTAL_API_KEY)

    def get_file_scan(self, target_name, target_files, target_string):
        if not self.VIRUS_TOTAL_API_KEY:
            logging.error('VirusTotal API key not set')
            return {}
        else:
            return modules.get_file_scan(target_name, target_files, target_string, self.VIRUS_TOTAL_API_KEY)

    def get_website_search(self, query, websites, max_results=10):
        """Passed query, list of file types and optionally int of max results wanted"""
        return modules.google_search(query, websites, 'site:', int(max_results))

    def get_document_search(self, query, filetypes, max_results=10):
        """Passed query, list of file types and optionally int of max results wanted"""
        return modules.google_search(query, filetypes, 'filetype:', int(max_results))
    
