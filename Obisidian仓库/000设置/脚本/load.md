```js RunJS="load" 
(() => {
    // 指定预览文件列表
    const previewFiles = [
        "统计.md",
    ];
	let leafTimer;
	const onActiveLeafChange = async (activeLeaf) => {
		// 定时防止无效触发，只取最后一个触发
		if(leafTimer) clearTimeout(leafTimer)
            leafTimer = setTimeout(async () => {
            // 排除非markdown视图类型
			const viewType = activeLeaf?.view.getViewType();
			if('markdown' !== viewType) return;
			// 获取文件路径
            const state = activeLeaf?.view.getState();
			const filePath = state.file
			if (!filePath) return;
			// 检查是否在指定文件列表中
            const isPreviewFile = previewFiles.some(item => filePath.includes(item));
            // 把文档设置为预览模式
            state.mode = isPreviewFile ? "preview" : "source";
            await activeLeaf?.setViewState({type: "markdown", state: state});
		}, 42);
	};
	this.app.workspace.on('active-leaf-change', onActiveLeafChange);
	onActiveLeafChange(this.app.workspace.activeLeaf);
})();
```