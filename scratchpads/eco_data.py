import wbdata
x =wbdata.get_indicators("NY.GDP.MKTP.CD", country="IN", data_date=("2015", "2023"))
print(x)