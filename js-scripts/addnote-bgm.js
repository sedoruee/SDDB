// ==UserScript==
// @name         SegumiOS Open Local Explorer from Bangumi
// @namespace    http://tampermonkey.net/
// @version      1.4
// @description  打开bangumi条目相对应的本地文件夹并在obsidian里添加相关笔记
// @author       Sedoruee
// @match        https://bgm.tv/subject/*
// @match        https://www.imdb.com/title/*
// @grant        GM_setClipboard
// @downloadURL https://update.greasyfork.org/scripts/513641/SegumiOS%20Open%20Local%20Explorer%20from%20Bangumi.user.js
// @updateURL https://update.greasyfork.org/scripts/513641/SegumiOS%20Open%20Local%20Explorer%20from%20Bangumi.meta.js
// ==/UserScript==

(function() {
    'use strict';

    const pageUrl = window.location.href;
    const todayDate = new Date().toISOString().slice(0, 10);
    const ahkLink = 'localexplorer:D:\\Obsidian\\.code\\python\\Gamecreat_bgmID.py';

    const subjectType = document.querySelector('.nameSingle > .grey')?.textContent;
    const subjectTitle = document.querySelector('.nameSingle > a')?.textContent;
    const subjectprofile = document.querySelector('div#subject_summary')?.textContent.replace(/\s+/g, ' ').trim();
    const tagsSelector = '.inner > a.l > span';
    const kindSelector = { 'Galgame': '视觉小说', '剧场版': '剧场版', 'TV': 'TV' };
    const nameSingleSelector = '.nameSingle';

    if (!subjectType) return;

    let nameSingle = document.querySelector(nameSingleSelector);
    if (!nameSingle) return;

    // 第一个按钮：打开本地文件夹
    let button1 = document.createElement('button');
    button1.textContent = '打开本地文件夹';
    button1.style.marginLeft = '10px';
    nameSingle.appendChild(button1);

    button1.addEventListener('click', function() {
        let tags = '', subjectKind = '';

        tags = Array.from(document.querySelectorAll(tagsSelector)).map(tagElement => `  - ${tagElement.textContent}`).join('\n');
        subjectKind = Object.keys(kindSelector).find(key => tags.includes(key));
        subjectKind = kindSelector[subjectKind] || '游戏';

        let formattedText = `
---
标题: ${subjectTitle}
链接: ${pageUrl}
类型: ${subjectType}
种类: ${subjectKind}
简介: "${subjectprofile}"
评分:
开始时间: ${todayDate}
结束时间:
用时:
tags:
${tags}
评价:
---

![[000设置/素材库/流程图：${subjectTitle}.canvas]]
![[000设置/素材库/读书笔记：${subjectTitle}.md]]
`;

        GM_setClipboard(formattedText.trim(), 'text');
        window.location.href = ahkLink;
    });

    // 第二个按钮：加入愿望单 (无条件出现)
    let button2 = document.createElement('button');
    button2.textContent = '加入愿望单';
    button2.style.marginLeft = '10px';
    nameSingle.appendChild(button2);

    button2.addEventListener('click', function() {
        let tags = '', subjectKind = '';
        tags = Array.from(document.querySelectorAll(tagsSelector)).map(tagElement => `  - ${tagElement.textContent}`).join('\n');
        subjectKind = Object.keys(kindSelector).find(key => tags.includes(key));
        subjectKind = kindSelector[subjectKind] || '游戏';

        let formattedText = `
---
标题: ${subjectTitle}
链接: ${pageUrl}
类型: ${subjectType}
种类: ${subjectKind}
简介: ${subjectprofile}
评分:
开始时间:
结束时间:
用时:
tags:
${tags}
评价:
---

![[000设置/素材库/流程图：${subjectTitle}.canvas]]
![[000设置/素材库/读书笔记：${subjectTitle}.md]]
`;

        GM_setClipboard(formattedText.trim(), 'text');
        window.location.href = ahkLink;
    });
})();