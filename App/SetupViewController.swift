import UIKit

final class SetupViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground

        let scrollView = UIScrollView()
        scrollView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(scrollView)

        let stack = UIStackView()
        stack.axis = .vertical
        stack.spacing = 20
        stack.translatesAutoresizingMaskIntoConstraints = false
        scrollView.addSubview(stack)

        addLabel("测试键盘", style: .largeTitle, to: stack)
        addLabel("离线安装验证 · 尚未接入 AI", style: .headline, to: stack)
        addLabel(
            "1. 打开设置 → 通用 → 键盘 → 键盘 → 添加新键盘，选择「测试键盘」。\n\n"
            + "2. 返回这里，点下方输入框，长按地球键，选择「测试键盘」。\n\n"
            + "3. 点「插入测试文字」，再验证「删除」和「切换键盘」。\n\n"
            + "4. 在备忘录和微信输入框重复测试。微信里先不要发送。",
            style: .body,
            to: stack
        )
        addLabel("本版本无需开启「允许完全访问」，不读取剪贴板、不联网、不保存输入内容。", style: .callout, to: stack)

        let textView = UITextView()
        textView.font = .preferredFont(forTextStyle: .body)
        textView.adjustsFontForContentSizeCategory = true
        textView.backgroundColor = .secondarySystemBackground
        textView.layer.cornerRadius = 12
        textView.textContainerInset = UIEdgeInsets(top: 12, left: 12, bottom: 12, right: 12)
        textView.accessibilityLabel = "键盘测试输入框"
        textView.heightAnchor.constraint(equalToConstant: 140).isActive = true
        stack.addArrangedSubview(textView)
        addLabel("固定测试文字：测试键盘已成功输入。", style: .footnote, to: stack)

        NSLayoutConstraint.activate([
            scrollView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            scrollView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor),
            scrollView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            scrollView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            stack.topAnchor.constraint(equalTo: scrollView.contentLayoutGuide.topAnchor, constant: 24),
            stack.bottomAnchor.constraint(equalTo: scrollView.contentLayoutGuide.bottomAnchor, constant: -24),
            stack.leadingAnchor.constraint(equalTo: scrollView.contentLayoutGuide.leadingAnchor, constant: 24),
            stack.trailingAnchor.constraint(equalTo: scrollView.contentLayoutGuide.trailingAnchor, constant: -24),
            stack.widthAnchor.constraint(equalTo: scrollView.frameLayoutGuide.widthAnchor, constant: -48),
        ])
    }

    private func addLabel(_ text: String, style: UIFont.TextStyle, to stack: UIStackView) {
        let label = UILabel()
        label.text = text
        label.font = .preferredFont(forTextStyle: style)
        label.adjustsFontForContentSizeCategory = true
        label.numberOfLines = 0
        stack.addArrangedSubview(label)
    }
}
