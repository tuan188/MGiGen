import MGArchitecture
import Reusable
import RxCocoa
import RxSwift
import UIKit

final class {{ name }}ViewController: UIViewController, Bindable {
    
    // MARK: - IBOutlets
    
    @IBOutlet weak var tableView: UITableView!
    
    // MARK: - Properties

    var viewModel: {{ name }}ViewModel!
    var disposeBag = DisposeBag()

    private var {{ enum.name_variable }}Sections = [{{ name }}ViewModel.{{ enum.name }}Section]()

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
            $0.rowHeight = 60
            $0.register(cellType: {{ enum.name }}Cell.self)
            $0.delegate = self
        }
    }
    
    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
            loadTrigger: Driver.just(()),
            select{{ enum.name }}Trigger: tableView.rx.itemSelected.asDriver()
        )
        
        let output = viewModel.transform(input, disposeBag: disposeBag)
        
        output.${{ enum.name_variable }}Sections
            .asDriver()
            .drive(onNext: { [unowned self] sections in
                self.{{ enum.name_variable }}Sections = sections
                self.tableView.reloadData()
            })
            .disposed(by: disposeBag)
    }
}

// MARK: - UITableViewDataSource
extension {{ name }}ViewController: UITableViewDataSource {
    func numberOfSections(in tableView: UITableView) -> Int {
        return {{ enum.name_variable }}Sections.count
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return {{ enum.name_variable }}Sections[section].{{ enum.name_variable }}List.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let {{ enum.name_variable }} = {{ enum.name_variable }}Sections[indexPath.section].{{ enum.name_variable }}List[indexPath.row]
        
        return tableView.dequeueReusableCell(for: indexPath, cellType: {{ enum.name }}Cell.self)
    }
    
    func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return {{ enum.name_variable }}Sections[section].title
    }
}

// MARK: - UITableViewDelegate
extension {{ name }}ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()  // TODO: - Replace with a specific storyboard
}
