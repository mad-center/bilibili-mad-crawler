import crawl_config as config
from src.year_stat import YearStat

year_stat = YearStat(config=config, year=2020)
year_stat.dump_all()
