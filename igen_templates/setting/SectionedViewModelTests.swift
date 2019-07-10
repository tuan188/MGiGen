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

        output.{{ enum.name_variable }}Sections.drive().disposed(by: disposeBag)
        output.selected{{ enum.name }}.drive().disposed(by: disposeBag)
    }

    func test_loadTriggerInvoked_load{{ enum.name }}List() {
        // act
        loadTrigger.onNext(())
        let {{ enum.name_variable }}Sections = try? output.{{ enum.name_variable }}Sections.toBlocking(timeout: 1).first()

        // assert
        XCTAssertEqual({{ enum.name_variable }}Sections?.count, 1)
    }

    private func indexPath(of {{ enum.name_variable }}: {{ name }}ViewModel.{{ enum.name }}) -> IndexPath? {
        let {{ enum.name_variable }}Sections = viewModel.{{ enum.name_variable }}Sections()
        for (section, {{ enum.name_variable }}Section) in {{ enum.name_variable }}Sections.enumerated() {
            for (row, a{{ enum.name }}) in {{ enum.name_variable }}Section.{{ enum.name_variable }}List.enumerated() {
                if a{{ enum.name }} == {{ enum.name_variable }} { // swiftlint:disable:this for_where
                    return IndexPath(row: row, section: section)
                }
            }
        }
        return nil
    }

{% for menu_case in enum.cases_title %}
    func test_select{{ enum.name }}TriggerInvoked_to{{ menu_case }}() {
        // act
        loadTrigger.onNext(())
        guard let indexPath = indexPath(of: .{{ enum.cases[loop.index0] }}) else {
            XCTFail()
            return
        }
        select{{ enum.name }}Trigger.onNext(indexPath)

        // assert
        XCTAssert(navigator.to{{ menu_case }}Called)
    }{{ '\n' if not loop.last }}
{% endfor %}
}
