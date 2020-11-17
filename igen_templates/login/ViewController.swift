import MGArchitecture
import Reusable
import RxCocoa
import RxSwift
import UIKit

final class {{ name }}ViewController: UIViewController, Bindable {
    
    // MARK: - IBOutlets
    @IBOutlet weak var usernameTextField: UITextField!
    @IBOutlet weak var usernameValidationLabel: UILabel!
    @IBOutlet weak var passwordTextField: UITextField!
    @IBOutlet weak var passwordValidationLabel: UILabel!
    @IBOutlet weak var loginButton: UIButton!
    
    // MARK: - Properties
    
    var viewModel: {{ name }}ViewModel!
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
        usernameValidationLabel.text = ""
        passwordValidationLabel.text = ""
    }

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
            usernameTrigger: usernameTextField.rx.text.orEmpty.asDriver(),
            passwordTrigger: passwordTextField.rx.text.orEmpty.asDriver(),
            loginTrigger: loginButton.rx.tap.asDriver()
        )
        
        let output = viewModel.transform(input, disposeBag: disposeBag)
        
        output.$usernameValidationMessage
            .asDriver()
            .drive(usernameValidationMessageBinder)
            .disposed(by: disposeBag)
        
        output.$passwordValidationMessage
            .asDriver()
            .drive(passwordValidationMessageBinder)
            .disposed(by: disposeBag)
        
        output.$isLoginEnabled
            .asDriver()
            .drive(loginButton.rx.isEnabled)
            .disposed(by: disposeBag)
        
        output.$isLoading
            .asDriver()
            .drive(rx.isLoading)
            .disposed(by: disposeBag)
        
        output.$error
            .asDriver()
            .unwrap()
            .drive(rx.error)
            .disposed(by: disposeBag)
    }
}

// MARK: - Binders
extension {{ name }}ViewController {
    var usernameValidationMessageBinder: Binder<String> {
        return Binder(self) { vc, message in
            vc.usernameValidationLabel.text = message
        }
    }
    
    var passwordValidationMessageBinder: Binder<String> {
        return Binder(self) { vc, message in
            vc.passwordValidationLabel.text = message
        }
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}
