import UIKit
import Reusable

final class {{ name }}ViewController: UIViewController, BindableType {
    @IBOutlet weak var tableView: UITableView!
    
    var viewModel: {{ name }}ViewModel!

    override func viewDidLoad() {
        super.viewDidLoad()
        configView()
    }

    private func configView() {
        tableView.do {
            $0.estimatedRowHeight = 550
            $0.rowHeight = UITableViewAutomaticDimension
        {% for p in properties %}
            $0.register(cellType: {{ model_name }}{{ p.name_title }}Cell.self)
        {% endfor %}
        }
    }
    deinit {
        logDeinit()
    }

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(loadTrigger: Driver.just(()))
        let output = viewModel.transform(input)
        output.cells
            .drive(tableView.rx.items) { tableView, index, cellType in
                let indexPath = IndexPath(row: index, section: 0)
                switch cellType {
            {% for p in properties %}
                case let .{{ p.name }}({{ p.name }}):
                    return tableView.dequeueReusableCell(
                        for: indexPath,
                        cellType: {{ model_name }}{{ p.name_title }}Cell.self)
            {% endfor %}
                }
            }
            .disposed(by: rx.disposeBag)
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}
