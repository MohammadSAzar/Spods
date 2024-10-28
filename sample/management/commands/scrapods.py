# from django.core.management.base import BaseCommand
# from sample.scrapers import scrape_all_podcasts, category_url_list, save_podcast_data_to_db
#
#
# class Command(BaseCommand):
#     help = 'Scrapes podcast data and saves it to the database.'
#
#     def handle(self, *args, **kwargs):
#         podcasts = scrape_all_podcasts(category_url_list)
#         for podcast in podcasts:
#             save_podcast_data_to_db(podcast)
#         self.stdout.write(self.style.SUCCESS('Successfully scraped and saved podcast data.'))
#
#
#
