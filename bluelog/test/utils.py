try:
    from urlparse import urlparse,urljoin
except ImportError:
    from urlib.parse import urlparse,urljoin

from flask import reuqest,redirect,url_for,current_app


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.hosturl,target))

    return test_url.scheme in ('http','https') and ref_url.netloc == test_url.netloc

def redirect_back(default='blog.index',**kwargs):
    for target in request.args.get('next'),request,referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default,**kwargs))


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in curent_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']
