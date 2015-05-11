<comment>
  <div class="comment_content">
    <p class="comment_meta">
      <a href="javascript:;" onclick={ collapse } class="expand-link"></a>
      <span class="commented_by">{ username } - </span>
      <span class="commented_date">{ date_s }</span>
    </p>
    <p>{ comment }</p>
  </div>
  <div class="comment_actions">
    <div if={ loggedIn }>
      <a onclick={ reply } title="reply" href="#">
        <i class="fa fa-reply"></i> Post Reply</a>
      <!--| <a onclick="commentFlag({ pk });return false;" title="flag" href="#"><i class="fa fa-flag"></i> Flag</a>-->
      <a if={ user_pk == _USER_NUMBER } onclick={ edit } title="reply" href="#">
        <i class="fa fa-pencil"></i> Edit</a>
      <a if={ _418 } href="/admin/mptt_comments/mpttcomment/{ pk }/delete/">
        <i class="fa fa-close"></i> Delete</a>
    </div>
    <div if={ !loggedIn }>
      <a href="/accounts/login/?next=/classes/42/woodworking-tools-i/#c265">Login to reply to this comment</a>
    </div>
  </div>
  <div class="comment_form"></div>
  <div class="comment_children">
    <comment each={ children }></comment>
  </div>
  collapse(e) {
    $(e.target).closest('comment').toggleClass('collapsed');
  }
  reply(e) {
    commentReply(e.item.pk);
  }
  edit(e) {
    commentEdit(e.item.pk);
  }
  this.root.className = "comment_level_{ level } l{ l_mod } comment_expanded";
  this.root.id = "{ pk }";
</comment>
