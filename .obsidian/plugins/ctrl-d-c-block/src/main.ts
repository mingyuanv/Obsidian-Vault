import { Plugin, Editor } from 'obsidian';

export default class CtrlDCBlockPlugin extends Plugin {
	async onload() {
		// 注册插入 C 代码块命令
		this.addCommand({
			id: 'insert-c-codeblock',
			name: '插入 C 语言代码块',
			editorCallback: (editor: Editor) => {
				this.insertCCodeBlock(editor);
			}
		});
	}

	/**
	 * 在光标位置插入 C 语言代码块
	 * @param editor Obsidian 编辑器对象
	 */
	private insertCCodeBlock(editor: Editor): void {
		const selection = editor.getSelection();
		const cursor = editor.getCursor();

		if (selection && selection.trim().length > 0) {
			// 有选中文本：包裹在代码块中
			const codeBlock = '```c\n' + selection + '\n```';
			editor.replaceSelection(codeBlock);
			// 光标定位到文本后的下一行
			const newPos = { line: cursor.line + 1, ch: 0 };
			editor.setCursor(newPos);
		} else {
			// 无选中文本：插入空代码块
			const codeBlock = '```c\n\n```';
			editor.replaceSelection(codeBlock);
			// 光标定位到代码块第一行
			const newPos = { line: cursor.line + 1, ch: 0 };
			editor.setCursor(newPos);
		}
	}

	onunload() {
		// 插件卸载时的清理工作
	}
}
