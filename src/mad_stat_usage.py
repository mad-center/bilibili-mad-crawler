import crawl_config as config
from src.mad_stat import MadStat

mad_stat = MadStat(config=config, year=2018)
mad_stat.dump_all()
