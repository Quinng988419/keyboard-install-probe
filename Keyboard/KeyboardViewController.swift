import UIKit

final class KeyboardViewController: UIInputViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .secondarySystemBackground

        let title = UILabel()
        title.text = "测试键盘 · 离线验证"
        title.font = .preferredFont(forTextStyle: .headline)
        title.adjustsFontForContentSizeCategory = true
        title.numberOfLines = 0

        let insertButton = UIButton(type: .system)
        var insertConfiguration = UIButton.Configuration.filled()
        insertConfiguration.title = "插入测试文字"
        insertConfiguration.cornerStyle = .medium
        insertButton.configuration = insertConfiguration
        insertButton.addTarget(self, action: #selector(insertTestText), for: .touchUpInside)

        let deleteButton = UIButton(type: .system)
        var deleteConfiguration = UIButton.Configuration.gray()
        deleteConfiguration.title = "删除"
        deleteButton.configuration = deleteConfiguration
        deleteButton.addTarget(self, action: #selector(deleteCharacter), for: .touchUpInside)

        let nextButton = UIButton(type: .system)
        var nextConfiguration = UIButton.Configuration.gray()
        nextConfiguration.title = "切换键盘"
        nextConfiguration.image = UIImage(systemName: "globe")
        nextConfiguration.imagePadding = 8
        nextButton.configuration = nextConfiguration
        nextButton.addTarget(
            self,
            action: #selector(handleInputModeList(from:with:)),
            for: .allTouchEvents
        )

        let controls = UIStackView(arrangedSubviews: [deleteButton, nextButton])
        controls.axis = .horizontal
        controls.spacing = 12
        controls.distribution = .fillEqually

        let stack = UIStackView(arrangedSubviews: [title, insertButton, controls])
        stack.axis = .vertical
        stack.spacing = 12
        stack.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(stack)

        let keyboardHeight = view.heightAnchor.constraint(equalToConstant: 230)
        keyboardHeight.priority = .defaultHigh
        NSLayoutConstraint.activate([
            keyboardHeight,
            stack.topAnchor.constraint(equalTo: view.topAnchor, constant: 16),
            stack.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
            stack.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -16),
            stack.bottomAnchor.constraint(lessThanOrEqualTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -12),
            insertButton.heightAnchor.constraint(greaterThanOrEqualToConstant: 48),
            deleteButton.heightAnchor.constraint(greaterThanOrEqualToConstant: 44),
            nextButton.heightAnchor.constraint(greaterThanOrEqualToConstant: 44),
        ])
    }

    @objc private func insertTestText() {
        textDocumentProxy.insertText("测试键盘已成功输入。")
    }

    @objc private func deleteCharacter() {
        textDocumentProxy.deleteBackward()
    }
}
