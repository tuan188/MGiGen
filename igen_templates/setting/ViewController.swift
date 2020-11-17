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
        
        output.${{ enum.name_variable }}List
            .asDriver()
            .drive(tableView.rx.items) { tableView, index, {{ enum.name_variable }} in
                return tableView.dequeueReusableCell(
                    for: IndexPath(row: index, section: 0),
                    cellType: {{ enum.name }}Cell.self)
                    .then {
                        $0.titleLabel.text = {{ enum.name_variable }}.description
                    }
            }
            .disposed(by: disposeBag)
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
