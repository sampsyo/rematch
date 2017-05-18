""" Random functions that didn't quite fit anywhere else. """

def disable_stale_posts():
    """ Triggered by a scheduler that is initialized in server/__init__.py
    Trigger interval can be set in the configuration file.
    """
    print 'Running stale post scheduler.'
    stale_posts = Post.get_posts(active_only=True, stale=True)
    print stale_posts
    for post in stale_posts:
        print 'Setting post %s to inactive.' % post['id']
        Post.update_post(post['id'], is_active=False)
        print 'We should notify %s' % post['contact_email']
