import MGArchitecture
import MGLoadMore
import Reusable
import RxCocoa
import RxSwift
import Then
import UIKit

final class {{ name }}ViewController: UIViewController, Bindable {

    // MARK: - IBOutlets

    @IBOutlet weak var tableView: PagingTableView!

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
        tableView.do {
            $0.register(cellType: {{ model_name }}Cell.self)
            $0.delegate = self
            $0.prefetchDataSource = self
            $0.estimatedRowHeight = 550
            $0.rowHeight = UITableView.automaticDimension
            {% if not paging %}
            $0.refreshFooter = nil
            {% endif %}
        }
    }

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
            loadTrigger: Driver.just(()),
            reloadTrigger: tableView.refreshTrigger,
            {% if paging %}
            loadMoreTrigger: tableView.loadMoreTrigger,
            {% endif %}
            select{{ model_name }}Trigger: tableView.rx.itemSelected.asDriver()
        )

        let output = viewModel.transform(input, disposeBag: disposeBag)

        output.${{ model_variable }}List
            .asDriver()
            .drive(tableView.rx.items) { tableView, row, {{ model_variable }} in
                return tableView.dequeueReusableCell(
                    for: IndexPath(row: row, section: 0),
                    cellType: {{ model_name }}Cell.self
                )
                .then {
                    $0.bindViewModel({{ model_variable }})
                }
            }
            .disposed(by: disposeBag)

        output.$error
            .asDriver()
            .unwrap()
            .drive(rx.error)
            .disposed(by: disposeBag)
        
        output.$isLoading
            .asDriver()
            .drive(rx.isLoading)
            .disposed(by: disposeBag)

        {% if paging %}
        output.$isLoadingMore
            .asDriver() 
            .drive(tableView.isLoadingMore)
            .disposed(by: disposeBag)

        {% endif %}
        output.$isEmpty
            .asDriver()
            .drive()
            .disposed(by: disposeBag)
    }
}

// MARK: - Binders
extension {{ name }}ViewController {

}

// MARK: - UITableViewDelegate
extension {{ name }}ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
    }
}

// MARK: - UITableViewDataSourcePrefetching
extension {{ name }}ViewController: UITableViewDataSourcePrefetching {
    func tableView(_ tableView: UITableView, prefetchRowsAt indexPaths: [IndexPath]) {

    }
    
    func tableView(_ tableView: UITableView, cancelPrefetchingForRowsAt indexPaths: [IndexPath]) {
        
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}
