# Create your tasks here
from __future__ import absolute_import, unicode_literals
import pytz
import logging
from datetime import timedelta, datetime

from django.conf import settings
from django.core.exceptions import ValidationError, FieldError

from celery import shared_task
from app.models import Post
from app.notification import *

logger = logging.getLogger("tasks")


@shared_task
def check_post_availability():

    logger.debug("Start task for checking post availability")

    posts = Post.objects.all()
    if posts:

        logger.debug("Have posts")
        unavailable_posts = []

        for post in posts:

            
            logger.debug("Working with {}".format(post.mac_uid))

            tz = pytz.timezone(settings.TIME_ZONE)
            now = tz.localize(datetime.now())
            av_time = now - timedelta(minutes=1)
            if post.last_seen < av_time and post.is_available:

                logger.info("Post {} isn't available".format(post.mac_uid))
                
                post.is_available = False
                unavailable_posts.append(post.mac_uid)

                try:
                    post.save()

                except (ValidationError, FieldError) as err:
                    logger.exception("Post isn't save with errors: {}".format(err))
        
        if unavailable_posts:
            
            logger.debug("{} posts are unavailable".format(unavailable_posts))

            sms_notification("{} posts are unavailable".format(unavailable_posts))
            email_notification("{} posts are unavailable".format(unavailable_posts))



    else:
        logger.warning("Posts not found")
