# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.contrib.auth import get_user_model
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse, resolve
from django.test import RequestFactory
from jackfrost.models import URLCollector, SitemapRenderer
import pytest


def test_medusa_renderer_repr():
    assert repr(SitemapRenderer(cls=1)) == '<jackfrost.models.SitemapRenderer sitemap_cls=1>'


@pytest.mark.django_db
def test_feed_renderer_support():
    class UserFeedProxy(get_user_model()):
        def get_absolute_url(self):
            return '/test/user/{}/'.format(self.pk)

        class Meta:
            proxy = True

    class UserFeed(Feed):
        def items(self):
            return UserFeedProxy.objects.all()

    users = [get_user_model().objects.create(username='u{}'.format(x))
             for x in range(1, 5)]
    user_pks = [u.pk for u in users]
    users_urls = [up.get_absolute_url()
                  for up in UserFeedProxy.objects.filter(pk__in=user_pks)]

    collector = URLCollector(renderers=(UserFeed,))
    assert frozenset(collector()) == frozenset(users_urls)