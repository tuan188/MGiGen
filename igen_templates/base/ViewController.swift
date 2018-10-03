import UIKit
import Reusable

final class {{ name }}ViewController: UIViewController, BindableType {
    var viewModel: {{ name }}ViewModel!

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    deinit {
        logDeinit()
    }

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input()
        let output = viewModel.transform(input)
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}
