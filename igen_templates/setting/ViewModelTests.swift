@testable import {{ project }}
import XCTest
import RxSwift
import RxBlocking

final class {{ name }}ViewModelTests: XCTestCase {

    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!

    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!

    private var disposeBag: DisposeBag!

    private let loadTrigger = PublishSubject<Void>()
    private let select{{ enum.name }}Trigger = PublishSubject<IndexPath>()

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase)

        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete(),
            select{{ enum.name }}Trigger: select{{ enum.name }}Trigger.asDriverOnErrorJustComplete()
        )

        output = viewModel.transform(input)

        disposeBag = DisposeBag()

        output.{{ enum.name_variable }}List.drive().disposed(by: disposeBag)
        output.selected{{ enum.name }}.drive().disposed(by: disposeBag)
    }

    func test_loadTriggerInvoked_load{{ enum.name }}List() {
        // act
        loadTrigger.onNext(())
        let {{ enum.name_variable }}List = try? output.{{ enum.name_variable }}List.toBlocking(timeout: 1).first()

        // assert
        XCTAssertEqual({{ enum.name_variable }}List?.count, {{ name }}ViewModel.{{ enum.name }}.allCases.count)
    }

    private func indexPath(of {{ enum.name_variable }}: {{ name }}ViewModel.{{ enum.name }}) -> IndexPath {
        return IndexPath(row: {{ enum.name_variable }}.rawValue, section: 0)
    }

{% for menu_case in enum.cases_title %}
    func test_select{{ enum.name }}TriggerInvoked_to{{ menu_case }}() {
        // act
        loadTrigger.onNext(())
        let indexPath = self.indexPath(of: .{{ enum.cases[loop.index0] }})
        select{{ enum.name }}Trigger.onNext(indexPath)

        // assert
        XCTAssert(navigator.to{{ menu_case }}Called)
    }{{ '\n' if not loop.last }}
{% endfor %}
}
