import Dto
import MGArchitecture
import Reusable
import RxCocoa
import RxSwift
import UIKit

final class {{ name }}ViewController: UITableViewController, Bindable {

    // MARK: - IBOutlets

    @IBOutlet weak var cancelButton: UIBarButtonItem!
    @IBOutlet weak var {{ submit }}Button: UIBarButtonItem!
    {% for p in properties %}
    {% if p.type.name == 'String' %}
    @IBOutlet weak var {{ p.name }}TextField: UITextField!
    {% endif %}
    {% endfor %}

    // MARK: - Properties

    var viewModel: {{ name }}ViewModel!
    var disposeBag = DisposeBag()

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

        let output = viewModel.transform(input, disposeBag: disposeBag)

        {% for p in properties %}
        output.${{ p.name }}
            .asDriver()
            .drive({{ (p.name + 'TextField.rx.text') if p.type.name == 'String'}})
            .disposed(by: disposeBag)

        {% endfor %}
        {% for p in properties %}
        output.${{ p.name }}Validation
            .asDriver()
            .drive({{ p.name }}ValidatorBinder)
            .disposed(by: disposeBag)

        {% endfor %}
        output.$is{{ submit_title }}Enabled
            .asDriver()
            .drive({{ submit }}Button.rx.isEnabled)
            .disposed(by: disposeBag)

        output.$error
            .asDriver()
            .drive()
            .disposed(by: disposeBag)

        output.$isLoading
            .asDriver()
            .drive()
            .disposed(by: disposeBag)
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
    static var sceneStoryboard = UIStoryboard()  // TODO: - Replace with a specific storyboard
}