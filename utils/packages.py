import csv


class PackagesUtils:
    @staticmethod
    def read_site_domain_names(operation='add'):
        site_domain_name = []
        if operation == 'edit':
            file_path = 'assets/packages/edit_package_sites_domain.csv'
        else:
            file_path = 'assets/packages/package_sites_domain.csv'
        with open(file_path) as csvfile:
            data = csv.reader(csvfile)
            next(data)
            for row in data:
                site_domain_name.append(row[0])
        return site_domain_name



