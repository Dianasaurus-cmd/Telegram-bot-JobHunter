import requests
from bs4 import BeautifulSoup
from functools import cached_property
class Vacancy:
    def __init__(self,name,experience,salary,pays,company,city):
        self.name = name
        self.experience = experience
        try:
            min_salary = salary[0].get('value')
            max_salary = salary[1].get('value')
            if min_salary.isdigit() and max_salary.isdigit(): salary  = f"{min_salary} - {max_salary}"
            else: salary = "-"
            self.salary = salary
            self.min_salary = min_salary
            self.max_salary = max_salary
        except (AttributeError,IndexError) as error:
            self.salary = "-"
            self.min_salary = "-"
            self.max_salary = '_'
        self.pays = pays
        self.company = company
        self.city = city
    def __str__(self):
        return f"Название : {self.name}\nОпыт : {self.name}\nЗарплата : {self.salary}\nВыплаты : {self.pays}\nКомпания : {self.company}\nГород : {self.city}"


class Search_for_jobes:
    @classmethod
    def generate(cls,page):
        page+=1
        url = f"https://hh.ru/search/vacancy?page={page}"
        headers = {'Host': 'hh.ru','User-Agent':'Safari','Accept': '*/*','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}
        response = requests.get(url,headers = headers)
        hh_soup = BeautifulSoup(response.text,'lxml')
        paginator = hh_soup.find('ol',class_ = 'vacancies-list--fKGBxTUjQkIkJ_iZ')
        vacancies = paginator.find_all('li')
        return_vacancies=  []
        for i in vacancies:
            vacancy = i
            vacancy = vacancy.find("div", class_ = 'vacancy-info--ieHKDTkezpEj0Gsx')
            try: name = vacancy.find("span",class_ = "magritte-text___tkzIl_7-1-37").text
            except AttributeError: name = "-"
            try: experience = vacancy.find("div",class_ = "magritte-tag__label___YHV-o_5-3-18").find('data').text
            except: experience = "-"
            try: 
                salary = vacancy.find("span",class_ = "magritte-text___pbpft_5-3-9 magritte-text_style-primary___AQ7MW_5-3-9 magritte-text_typography-label-1-regular___pi3R-_5-3-9").find_all('data')
            except (AttributeError,IndexError) as error: salary = "-"
            try: 
                pays = vacancy.find("div",class_ = "magritte-tag___WdGxk_5-3-18 magritte-tag_style-neutral___cw1Bt_5-3-18 magritte-tag_size-medium___Splpy_5-3-18").find('div',class_= 'magritte-tag__label___YHV-o_5-3-18').find('span').text
            except AttributeError:
                pays = "-"
            try:
                company = vacancy.find("div",class_ = "info-section--YaC_npvTFcwpFd1I").find('a',class_ = "magritte-link___b4rEM_7-1-37 magritte-link_mode_primary___l6una_7-1-37 magritte-link_style_neutral___iqoW0_7-1-37").find('span',class_ = "magritte-text___tkzIl_7-1-37").text
            except AttributeError:
                company = "-"
            try:
                city = vacancy.find("div",class_ = "info-section--YaC_npvTFcwpFd1I").find("address",class_ = "address--sQo6S3UaqQUt843N").find('span',class_ = "magritte-text___pbpft_5-3-9 magritte-text_style-primary___AQ7MW_5-3-9 magritte-text_typography-label-3-regular___Nhtlp_5-3-9").text
            except AttributeError:
                city = "-"
            return_vacancies.append(Vacancy(name,experience,salary,pays,company,city))
        return return_vacancies

    @classmethod
    def search_name(cls,name,page = -1):
        vacancies= cls.generate(page)
        show = [Vacancy.__str__(vacancy) for vacancy in vacancies if name.lower() in vacancy.name.lower()]
        return [show,page+1] if show else [['Ничего не нашлось'],page+1]
    @classmethod
    def search_city(cls,city,page = -1):
        vacancies = cls.generate(page)
        show =  [Vacancy.__str__(vacancy) for vacancy in vacancies if city.lower() in vacancy.city.lower()]
        return [show,page+1] if show else [['Ничего не нашлось'],page+1]
    @classmethod
    def search_company(cls,company,page = -1):
        vacancies = cls.generate(page)
        show =  [Vacancy.__str__(vacancy) for vacancy in vacancies if company.lower() in vacancy.company.lower()]
        return [show,page+1] if show else [['Ничего не нашлось'],page+1]
    @classmethod
    def search_salary(cls,salary,page = -1):
        if salary.isdigit():
            vacancies = cls.generate(page)
            show = [Vacancy.__str__(vacancy) for vacancy in vacancies if vacancy.min_salary.isdigit() and vacancy.max_salary.isdigit() and int( vacancy.min_salary)<=int(salary)<=int(vacancy.max_salary)]
        else : show = "Вы ввели неккоректную зарплату)"
        return [show,page+1] if show else [['Ничего не нашлось'],page+1]
    @cached_property
    def generate_all_vacancies(self,page = -1):
        vacancy_list = []
        while page !=38:
            print(page)
            vacancies = Search_for_jobes.generate(page)
            page +=1
            vacancy_list.extend(vacancies)
        
        return vacancy_list
    @classmethod
    def view_top_10(cls):
        helper = Search_for_jobes()
        vacancy_list = helper.generate_all_vacancies
        top_10 =sorted([i for i in vacancy_list if i.max_salary.isdigit()], key = lambda x: int(x.max_salary),reverse = True)
        return [f"Место {top_10.index(i)+1}\n{Vacancy.__str__(i)}" for i in top_10[:10]]


print(Search_for_jobes.view_top_10())