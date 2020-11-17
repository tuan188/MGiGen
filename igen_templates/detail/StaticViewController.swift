import MGArchitecture
import Reusable
import RxCocoa
import RxSwift
import UIKit

final class {{ name }}ViewController: UITableViewController, Bindable {

    // MARK: - IBOutlets

    {% for p in properties %}
    @IBOutlet weak var {{ p.name }}Label: UILabel!
    {% endfor %}

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

    }

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
            loadTrigger: Driver.just(())
        )

        let output = viewModel.transform(input, disposeBag: disposeBag)

        {% for p in properties %}
        output.${{ p.name }}
            .asDriver()
            .drive()
            .disposed(by: disposeBag)

        {% endfor %}
    }
}

// MARK: - Binders
extension {{ name }}ViewController {

}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}
