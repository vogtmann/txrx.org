<comment-form>
  <form action={ opts.form_url } method="POST" onsubmit="commentPost(this);return false;"
        class="comment_form_wrapper">
    <div class="comment_form">
      <p>Comments are displayed using Markdown.</p>
      <a href="javascript:;" onclick="$(this).next().toggleClass('show')">Show Formatting help</a>
      <table class="md" cellpadding="3">
        <tbody>
          <tr style="background-color: #ffff99; text-align: center">
            <td><em>you type:</em></td>
            <td><em>you see:</em></td>
          </tr>
          <tr>
            <td>*italics*</td><td><em>italics</em></td>
          </tr>
          <tr>
            <td>**bold**</td>
            <td><b>bold</b></td>
          </tr>
          <tr>
            <td>[txrx!](http://txrxlabs.org)</td>
            <td><a href="http://txrxlabs.org">txrx!</a></td>
          </tr>
          <tr>
            <td>http://txrxlabs.org</td>
            <td><a href="http://txrxlabs.org">http://txrxlabs.org</a></td>
          </tr>
          <tr>
            <td>* item 1<br>* item 2<br>* item 3</td>
            <td><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></td>
          </tr>
          <tr>
            <td>&gt; quoted text</td>
            <td><blockquote>quoted text</blockquote></td>
          </tr>
          <tr>
            <td>Lines starting with four spaces<br>are treated like code:<br><br><span class="spaces">&nbsp;&nbsp;&nbsp;&nbsp;</span>if 1 * 2 &lt; 3:<br><span class="spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>print "hello, world!"<br></td>
            <td>Lines starting with four spaces<br>are treated like code:<br><pre>if 1 * 2 &lt; 3:<br>&nbsp;&nbsp;&nbsp;&nbsp;print "hello, world!"</pre></td>
          </tr>
        </tbody>
      </table>

      <fieldset>
        <ul class="list-unstyled">
          <li class="required">
            <textarea cols="40" id="id_comment" name="comment" rows="10">{ opts.comment }</textarea>
          </li>
          <li>
            <input id="id_content_type" name="content_type" type="hidden" value={ opts.content_type } />
            <input id="id_object_pk" name="object_pk" type="hidden" value={ opts.object_pk } />
            <input id="id_parent_pk" name="parent_pk" type="hidden" value={ opts.parent_pk } />
            <input id="id_comment_pk" name="comment_pk" type="hidden" value={ opts.pk } />
            <input type="submit" name="submit" class="submit-post" value="Post" />
          </li>
        </ul>
      </fieldset>

    </div>
  </form>

</comment-form>
