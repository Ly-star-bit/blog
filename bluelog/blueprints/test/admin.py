import os
from flask import render_template,flash,redirect,url_for,request,current_app,Blueprint,send_from_directory
from flask_login import login_required,current_user
from flask_ckeditor import upload_success,upload_fail

from bluelog.extensions import db
from bluelog.forms import SettingForm,PostForm,CategotyForm,LinkForm
from bluelog.models import Post,Categoty,Comment,Link
from bluelog.utils import redirect_back,allowed_file

admin_bp = Blueprint('admin',__name__)
@admin_bp.route('/settings',methods=["GET","POST"])
@login_required
def setting():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.blog_title=form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data

        db.session.commit()
        flash("Setting updated.","success")
        return redirect(url_for("blog.index"))

    form.name.data = current_user.name
    form.blog_title.data = curent_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html',form=form)
@admin_bp.route('post/manage')
@login_required
def manage_post():
    page = request.args.get('page',1,type = int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config('BLUELOG_MANAGE_POST_PER_PAGE')
    posts = pagination.items
    return render_template('admin/manage_post.html',page=page,pagination=paginaiton)


@admin_bp.route('post/new',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        category = Categoty.qury.get(form.categoty.data)
        post = Post(title = title,body = body,categoty = category)


        db.session.add(post)
        db.session.commit()
        flash('Post created','success')
        return redierct(url_for('blog.show_post'),post_id = post.id())
    return render_template('admin/new_post.html',form=form)
@admin_bp.route('/post/<int:post_id>/edit',methods=['GET','POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post=Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash("Post updated","success")
        return redirect(url_for('blog.show_post',post_id=post.id)
    form.title.data= post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html',form=form)
@admin_bp.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.','success')
    return redirect_back()

@admin_bp.route('/post/<int:post_id>/set-comment',methods=['POST']
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment():
        post.can_comment = Flase
        flash('Comment diabled.','success')
    else:
        post.can_comment = True
        flash('Comment enabled.','success')
    db.session.commit()
    return redirect_back()



@admin_bp.route('/comment/manage')
@login_required

def manage_comment():
    filter_rule = request.args.get('filter','all')
    page = request.args.get('page',1,type = int)
    per_page = current.app.config('BLUEBLOG_COMMENT_PER_PAGE')
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed = False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin = True)

    else:
        filtered_comments = Comment_query

    pagination = filtered_comments.order_by(Commnet.timestamp.desc()).paginate(page,per_page = per_page)
    comments = pagination.items

    return render_template('admin/manage_comment.html',comments = comments,pagination =paginaiton)


@admin_bp.route('/comment/<int:comment_id>/approve',methods = ['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment published.','sucess')
    return redirect_back()

@admin_bp.route('/comment/<int:comment_id>/delete',methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment）
    db.session.commit()
    flash('Comment deleted.','success')
    return redirect_back()

@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')

@admin_bp.route('categoty/new',methods = ["GET","POST"])
@login_required

def new_category():
    form = CategotyForm()
    if form.validate_on_submit():
         name = form.name.data
         category = Category(name=name)
         db.session.add(category)
         db.session.commit()
         flash('Category created.','success')
         return redirect(url_for('.manage_category'))


    return render_template('admin/new_categoty.html',form=form)

@admin_bp.route('category/<int:categoty_id>/edit',methods=['GET','POST']
@login_required
def edit_categoty(categoty_id):
    form = CategoryForm()
    category=Category.query.get_or_404(category_id)
    if category.id ==1:

        flash('you can not edit the default category.','warning')
        return redirect(url_for('blog.index')
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated.','success')
        return redirect(url_for('.manage_category'))

    form.name.data = category.name
    return render_template('admin/edit_category.html',form = form)

@admin_bp.route('/category/<int:category_id>/delete',methods = ['POST'])
@login_required
def delete_category(category_id)：
    category = Category.query.get_or_404(category_id)
    if category.id ==1:
        flash('you can not delete the default category.','warning')
        return  redirect(url_for('blog.index'))
    category.delete()
    flash('Category deleted.','success')
    return redirect(url_for('.manage_category'))



@admin_bp.route('/link/manage')
@login_required
def manage_link():
    return render_template('admin/manage_link.html')

@admin_bp.route('/link/manage/new',methods=["GET","POST"])
@login_required
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        link = Link(name=name,url = url)
        db.session.add(link)
        db.session.commit()
        flash('Link created.','success')
        return redirect(url_for('.manage_link')
    return render_template('admin/new_link.html',form = form)


@admin_bp.route('/link/<int:link_id>/edit',methods=['GET','POST'])
@login_required

def edit_link(link_id):
    form = LinkForm()
    link = Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
        flash('Link updated.','success')
        return redirect(url_for('.manage_link'))

    form.name.data = link.name
    form.url.data = link.url
    return render_template('admin/edit_link.html',form = form)

@admin_bp.route('/link/<int:link_id>/delete',methods = ['POST'])
@login_required
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link deleted.','success')
    return redirect(url_for('.manage_link'))

@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current.app.config['BLUELOG_UPLOAD_PATH'],filename)

@admin_bp.route('/upload',methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('Image only')
    f.save(os.path.join(current_app.config['BLUELOG_UPLOAD_PAT'],f.filename))
    url = url_for('.get_image',filename = f.filename)
    return upload_success(url,f.filename)
