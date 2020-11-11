import Dto
import MGArchitecture
import Reusable
import RxCocoa
import RxSwift
import UIKit

final class {{ name }}ViewController: UIViewController, Bindable {

    // MARK: - IBOutlets

    @IBOutlet weak var cancelButton: UIBarButtonItem!
    @IBOutlet weak var {{ submit }}Button: UIBarButtonItem!
    @IBOutlet weak var tableView: UITableView!

    // MARK: - Properties

    var viewModel: {{ name }}ViewModel!
    var disposeBag = DisposeBag()

    {% for p in properties %}
    {% if p.type.name == 'String' %}
    private weak var {{ p.name }}TextField: UITextField?
    private weak var {{ p.name }}ValidationLabel: UILabel?
    {% endif %}
    {% endfor %}

    {% for p in properties %}
    {% if p.type.name != 'String' %}
    private let {{ p.name }}Trigger = PublishSubject<{{ p.type.name }}>()
    {% endif %}
    {% endfor %}

    private let dataTrigger = PublishSubject<{{ name }}ViewModel.DataType>()
    private let endEditTrigger = PublishSubject<Void>()
    private var cells = [{{ name }}ViewModel.CellType]()

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
        tableView.do {
            $0.rowHeight = 70
            {% for p in properties %}
            $0.register(cellType: {{ name }}{{ p.name_title }}Cell.self)
            {% endfor %}
            $0.tableFooterView = UIView()
            $0.keyboardDismissMode = .onDrag
            $0.dataSource = self
        }
    }

    func bindViewModel() {
        let loadTrigger = endEditTrigger
            .map { {{ name }}ViewModel.TriggerType.endEditing }
            .asDriverOnErrorJustComplete()
            .startWith({{ name }}ViewModel.TriggerType.load)

        let input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger,
            {{ submit }}Trigger: {{ submit }}Button.rx.tap.asDriver(),
            cancelTrigger: cancelButton.rx.tap.asDriver(),
            dataTrigger: dataTrigger.asDriverOnErrorJustComplete()
        )

        let output = viewModel.transform(input, disposeBag: disposeBag)

        output.$cells
            .asDriver()
            .drive(cellsBinder)
            .disposed(by: disposeBag)

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
    }

    {% endfor %}
    var cellsBinder: Binder<([{{ name }}ViewModel.CellType], needReload: Bool)> {
        return Binder(self) { vc, args in
            let (cells, needReload) = args
            vc.cells = cells
            if needReload {
                vc.tableView.reloadData()
            }
        }
    }
}

// MARK: - UITableViewDataSource
extension {{ name }}ViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return cells.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cellType = cells[indexPath.row]
        let viewModel = ValidationResultViewModel(validationResult: cellType.validationResult)

        switch cellType.dataType {
        {% for p in properties %}
        case let .{{ p.name }}({{ p.name }}):
            let cell = tableView.dequeueReusableCell(for: indexPath, cellType: {{ name }}{{ p.name_title }}Cell.self)
            {% if p.type.name == 'String' %}

            cell.{{ p.name }}TextField.rx.text.orEmpty
                .subscribe(onNext: { [unowned self] text in
                    self.dataTrigger.onNext({{ name }}ViewModel.DataType.{{ p.name }}(text))
                })
                .disposed(by: cell.disposeBag)

            cell.{{ p.name }}TextField.rx.controlEvent(UIControl.Event.editingDidEnd)
                .subscribe(onNext: { [unowned self] _ in
                    self.endEditTrigger.onNext(())
                })
                .disposed(by: cell.disposeBag)

            {{ p.name }}TextField = cell.{{ p.name }}TextField
            {{ p.name }}ValidationLabel = cell.{{ p.name }}ValidationLabel
            {% endif %}

            return cell
        {% endfor %}
        }
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}