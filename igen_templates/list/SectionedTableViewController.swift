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

    private var {{ model_variable }}Sections = [{{ name }}ViewModel.{{ model_name }}SectionViewModel]()

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

        output.${{ model_variable }}Sections
            .asDriver()
            .drive(onNext: { [unowned self] sections in
                self.{{ model_variable }}Sections = sections
                self.tableView.reloadData()
            })
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
        
        output.$isReloading
            .asDriver()
            .drive(tableView.isRefreshing)
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

// MARK: - UITableViewDataSource
extension {{ name }}ViewController: UITableViewDataSource {
    func numberOfSections(in tableView: UITableView) -> Int {
        return {{ model_variable }}Sections.count
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return {{ model_variable }}Sections[section].{{ model_variable }}List.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let {{ model_variable }} = {{ model_variable }}Sections[indexPath.section].{{ model_variable }}List[indexPath.row]
        
        return tableView.dequeueReusableCell(for: indexPath,
                                             cellType: {{ model_name }}Cell.self)
            .then {
                $0.bindViewModel({{ model_variable }})
            }
    }
}

// MARK: - UITableViewDelegate
extension {{ name }}ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
    }
    
    func tableView(_ tableView: UITableView, heightForFooterInSection section: Int) -> CGFloat {
        return CGFloat.leastNonzeroMagnitude
    }
    
    func tableView(_ tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
        return 44
    }
    
    func tableView(_ tableView: UITableView, viewForHeaderInSection section: Int) -> UIView? {
        let header = tableView.dequeueReusableHeaderFooterView({{ model_name }}HeaderView.self)
        header?.titleLabel.text = {{ model_variable }}Sections[section].header
        return header
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
