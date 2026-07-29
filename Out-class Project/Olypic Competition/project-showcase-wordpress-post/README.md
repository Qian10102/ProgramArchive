# Olympic AI：WordPress 文章导入包

这个目录将原 `project-showcase` 的单页网站重组为一篇普通 WordPress **文章（Post）**。它不包含主题文件，也不会修改或替换 `qinglan-blog`；发布后会使用当前主题的 `single.php` 文章页。

## 文件说明

- `post-content.html`：文章正文。将全部内容粘贴至 WordPress 编辑器的“自定义 HTML”区块即可。
- `post-styles.css`：仅使用 `.project-showcase-post` 前缀的文章样式，不影响其他文章。
- `assets/`：正文中使用的四张项目结果图。

## 发布到 WordPress

1. 后台进入“媒体 → 添加媒体文件”，上传 `assets/` 内的四张 PNG 文件。
2. 新建“文章”，标题建议为 `Olympic AI：智能传感器预测性维护项目`；可归入“个人项目”分类。
3. 添加一个“自定义 HTML”区块，粘贴 `post-content.html` 全部内容。
4. 将正文中四个 `src="assets/..."` 替换成媒体库中相应图片的完整 URL。
5. 将 `post-styles.css` 追加到当前主题的样式表，或通过“额外 CSS”功能添加。若需只加载给这篇文章，可在子主题中按文章 slug 条件加载该文件。
6. 为文章设置特色图片（建议使用 `assets/forecast-area.png`），然后发布。

## 在 qinglan-blog 中按文章加载样式（可选）

将 `post-styles.css` 放到主题的 `assets/` 目录，并在 `functions.php` 的 `wp_enqueue_scripts` 回调内加入：

```php
if (is_single('olympic-ai')) {
    wp_enqueue_style(
        'olympic-ai-post',
        get_template_directory_uri() . '/assets/olympic-ai-post.css',
        ['qinglan-style'],
        '1.0.0'
    );
}
```

发布文章时将固定链接设置为 `olympic-ai` 即可。若使用其它 slug，请同步修改 `is_single()` 中的值。
