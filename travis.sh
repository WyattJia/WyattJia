#!/usr/bin/env bash
set -e # halt script on error

echo 'Testing travis...'
bundle exec jekyll build
bundle exec htmlproofer ./_site --only-4xx

<li class="item"> <a class="link" href="https://www.douban.com/people/bitstring">Douban</a> </li>
<li class="item"> <a class="link" href="http://music.163.com/#/user/home?id=188483">Music</a> </li>