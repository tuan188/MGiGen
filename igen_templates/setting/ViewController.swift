import UIKit
import Reusable
import RxDataSources

final class {{ name }}ViewController: UIViewController, BindableType {
    
    // MARK: - IBOutlets
    
    @IBOutlet weak var tableView: UITableView!
    
    // MARK: - Properties

    var viewModel: {{ name }}ViewModel!
    
    private typealias {{ name }}{{ enum.name }}SectionModel = SectionModel<String, {{ name }}ViewModel.{{ enum.name }}>
    private var dataSource: RxTableViewSectionedReloadDataSource<{{ name }}{{ enum.name }}SectionModel>?
    
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
        
        let output = viewModel.transform(input)
        
        let dataSource = RxTableViewSectionedReloadDataSource<{{ name }}{{ enum.name }}SectionModel>(
            configureCell: { (_, tableView, indexPath, {{ enum.name_variable }}) -> UITableViewCell in
                return tableView.dequeueReusableCell(for: indexPath, cellType: {{ enum.name }}Cell.self)
                    .then {
                        $0.titleLabel.text = {{ enum.name_variable }}.description
                    }
            }, titleForHeaderInSection: { dataSource, section in
                return dataSource.sectionModels[section].model
            })
        
        self.dataSource = dataSource
        
        output.{{ enum.name_variable }}Sections
            .map {
                $0.map { section in
                    {{ name }}{{ enum.name }}SectionModel(model: section.title, items: section.{{ enum.name_variable }}List)
                }
            }
            .drive(tableView.rx.items(dataSource: dataSource))
            .disposed(by: rx.disposeBag)
        
        output.selected{{ enum.name }}
            .drive()
            .disposed(by: rx.disposeBag)
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}

// MARK: - UITableViewDelegate
extension {{ name }}ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
    }
}