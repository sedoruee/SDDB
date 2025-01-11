<%*
  // 获取剪贴板内容
  const clipboardContent = await navigator.clipboard.readText();

  // 输出剪贴板内容到当前活动窗口
  tR += clipboardContent;
%>