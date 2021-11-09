db_name = 'bilibili'
mongodb_url = 'mongodb://127.0.0.1:27017/'

# reference: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/video/video_zone.md

# ==============================================================
primary_partition_code = 'douga'

subpartition_name = 'MAD·AMV'
subpartition_code = 'mad'
subpartition_tid = 24

crawl_progress_collection_name = ' multi_crawl_mad_by_init_tag'

# ============================================================
# 完结动画	finish	32	已完结的动画番剧合集	/v/anime/finish
# primary_partition_code = 'anime'
#
# subpartition_name = '完结动画'
# subpartition_code = 'finish'
# subpartition_tid = 32
#
# crawl_progress_collection_name = 'multi_crawl_finish_by_init_tag'
# ===========================================================
