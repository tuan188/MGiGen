//___FILEHEADER___

import UIKit
import MGArchitecture
import RxSwift
import RxCocoa
import Reusable
import Then

final class ___VARIABLE_productName___ViewController: UIViewController, Bindable {
    
    // MARK: - IBOutlets
    
    // MARK: - Properties
    
    var viewModel: ___VARIABLE_productName___ViewModel!
    var disposeBag = DisposeBag()
    
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
        let input = ___VARIABLE_productName___ViewModel.Input()
        let output = viewModel.transform(input, disposeBag: disposeBag)
    }
}

// MARK: - Binders
extension ___VARIABLE_productName___ViewController {
    
}

// MARK: - StoryboardSceneBased
extension ___VARIABLE_productName___ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}
