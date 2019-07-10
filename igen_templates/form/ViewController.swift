import UIKit
import Reusable

final class {{ name }}ViewController: UITableViewController, BindableType {

    // MARK: - IBOutlets

    @IBOutlet weak var cancelButton: UIBarButtonItem!
    @IBOutlet weak var {{ submit }}Button: UIBarButtonItem!
    {% for p in properties %}
    {% if p.type.name == 'String' %}
    @IBOutlet weak var nameTextField: UITextField!
    {% endif %}
    {% endfor %}

    // MARK: - Properties

    var viewModel: {{ name }}ViewModel!

    {% for p in properties %}
    {% if p.type.name != 'String' %}
    private let {{ p.name }}Trigger = PublishSubject<{{ p.type.name }}>()
    {% endif %}
    {% endfor %}

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
        let input = {{ name }}ViewModel.Input(
            loadTrigger: Driver.just(()),
            {% for p in properties %}
            {% if p.type.name == 'String' %}
            {{ p.name }}Trigger: {{ p.name }}TextField.rx.text.orEmpty.asDriver(),
            {% else %}
            {{ p.name }}Trigger: {{ p.name }}Trigger.asDriverOnErrorJustComplete(),
            {% endif %}
            {% endfor %}
            {{ submit }}Trigger: {{ submit }}Button.rx.tap
                .throttle(RxTimeInterval.milliseconds(500), scheduler: MainScheduler.instance)
                .asDriverOnErrorJustComplete(),
            cancelTrigger: cancelButton.rx.tap
                .throttle(RxTimeInterval.milliseconds(500), scheduler: MainScheduler.instance)
                .asDriverOnErrorJustComplete()
        )

        let output = viewModel.transform(input)

        {% for p in properties %}
        output.{{ p.name }}
            .drive({{ (p.name + 'TextField.rx.text') if p.type.name == 'String'}})
            .disposed(by: rx.disposeBag)

        {% endfor %}
        {% for p in properties %}
        output.{{ p.name }}Validation
            .drive({{ p.name }}ValidatorBinder)
            .disposed(by: rx.disposeBag)

        {% endfor %}
        output.is{{ submit_title }}Enabled
            .drive({{ submit }}Button.rx.isEnabled)
            .disposed(by: rx.disposeBag)

        output.{{ submit }}
            .drive()
            .disposed(by: rx.disposeBag)

        output.cancel
            .drive()
            .disposed(by: rx.disposeBag)

        output.error
            .drive(rx.error)
            .disposed(by: rx.disposeBag)

        output.isLoading
            .drive(rx.isLoading)
            .disposed(by: rx.disposeBag)
    }

}

// MARK: - Binders
extension {{ name }}ViewController {
    {% for p in properties %}
    var {{ p.name }}ValidatorBinder: Binder<ValidationResult> {
        return Binder(self) { vc, validation in

        }
    } {{ '\n' if not loop.last }}
    {% endfor %}
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}