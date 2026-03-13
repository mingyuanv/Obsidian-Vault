"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const obsidian_1 = require("obsidian");
class CtrlDCBlockPlugin extends obsidian_1.Plugin {
    onload() {
        return __awaiter(this, void 0, void 0, function* () {
            // 注册插入 C 代码块命令
            this.addCommand({
                id: 'insert-c-codeblock',
                name: '插入 C 语言代码块',
                editorCallback: (editor) => {
                    this.insertCCodeBlock(editor);
                }
            });
        });
    }
    /**
     * 在光标位置插入 C 语言代码块
     * @param editor Obsidian 编辑器对象
     */
    insertCCodeBlock(editor) {
        const selection = editor.getSelection();
        const cursor = editor.getCursor();
        if (selection && selection.trim().length > 0) {
            // 有选中文本：包裹在代码块中
            const codeBlock = '```c\n' + selection + '\n```';
            editor.replaceSelection(codeBlock);
            // 光标定位到文本后的下一行
            const newPos = { line: cursor.line + 1, ch: 0 };
            editor.setCursor(newPos);
        }
        else {
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
exports.default = CtrlDCBlockPlugin;
