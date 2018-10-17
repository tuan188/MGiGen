import UIKit
import Reusable

final class {{ name }}ViewController: UIViewController, BindableType {
    
    // MARK: - IBOutlets
    
    // MARK: - Properties
    
    var viewModel: {{ name }}ViewModel!

    // MARK: - Life Cycle
    
    override func viewDidLoad() {
        super.viewDidLoad()
        configView()
    }

    deinit {
        logDeinit()
    }
    
    // MARK: - Methods

    private func configView() {
        
    }

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input()
        let output = viewModel.transform(input)
    }
}

// MARK: - Binders
extension {{ name }}ViewController {

}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}
