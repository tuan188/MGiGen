@testable import {{ project }}
import Dto
import RxSwift
import ValidatedPropertyKit
import XCTest

final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!
    private var disposeBag: DisposeBag!

    // Triggers
    {% for p in properties %}
    private let {{ p.name }}Trigger = PublishSubject<{{ p.type.name }}>()
    {% endfor %}
    private let loadTrigger = PublishSubject<Void>()
    private let {{ submit }}Trigger = PublishSubject<Void>()
    private let cancelTrigger = PublishSubject<Void>()

    private var {{ model_variable }}: {{ model_name }}!

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        {{ model_variable }} = {{ model_name }}()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase, {{ model_variable }}: {{ model_variable }})

        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete(),
        {% for p in properties %}
            {{ p.name }}Trigger: {{ p.name }}Trigger.asDriverOnErrorJustComplete(),
        {% endfor %}
            {{ submit }}Trigger: {{ submit }}Trigger.asDriverOnErrorJustComplete(),
            cancelTrigger: cancelTrigger.asDriverOnErrorJustComplete()
        )

        disposeBag = DisposeBag()
        output = viewModel.transform(input, disposeBag: disposeBag)
    }

    func test_loadTrigger_show{{ model_name }}() {
        // act
        loadTrigger.onNext(())

        // assert
        {% for p in properties %}
        XCTAssertEqual(output.{{ p.name }}, {{ model_variable }}.{{ p.name }})
        {% endfor %}
    }

    func test_loadTrigger_enable_{{ submit }}_byDefault() {
        // act
        loadTrigger.onNext(())

        // assert
        XCTAssertEqual(output.is{{ submit_title }}Enabled, true)
    }

    {% for p in properties %}
    func test_{{ p.name }}Trigger_validate{{ p.name_title }}() {
        // act
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssert(useCase.validate{{ p.name_title }}Called)
    }

    func test_{{ p.name }}Trigger_validate{{ p.name_title }}FailNotEnable_{{ submit }}() {
        // arrange
        useCase.validate{{ p.name_title }}ReturnValue = ValidationResult.failure(ValidationError(message: ""))

        // act
        {% for p in properties %}
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {% endfor %}
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssertEqual(output.is{{ submit_title }}Enabled, false)
    } {{ '\n' if not loop.last }}
    {% endfor %}

    func test_enable_{{ submit }}() {
        // act
        {% for p in properties %}
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {% endfor %}
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssertEqual(output.is{{ submit_title }}Enabled, true)
    }

    func test_{{ submit }}Trigger_not_{{ submit }}() {
        // arrange
        {% if properties %}
        useCase.validate{{ properties[0].name_title }}ReturnValue = ValidationResult.failure(ValidationError(message: ""))
        {% endif %}

        // act
        {% for p in properties %}
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {% endfor %}
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssertFalse(useCase.{{ submit }}Called)
    }

    func test_{{ submit }}Trigger_{{ submit }}() {
        // act
        {% for p in properties %}
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {% endfor %}
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssert(useCase.{{ submit }}Called)
        XCTAssert(navigator.dismissCalled)
    }

    func test_{{ submit }}Trigger_{{ submit }}FailShowError() {
        // arrange
        useCase.{{ submit }}ReturnValue = Observable.error(TestError())

        // act
        {% for p in properties %}
        {{ p.name }}Trigger.onNext({{ p.type.mock_value }})
        {% endfor %}
        {{ submit }}Trigger.onNext(())

        // assert
        XCTAssert(useCase.{{ submit }}Called)
        XCTAssertFalse(navigator.dismissCalled)
        XCTAssert(output.error is TestError)
    }

    func test_cancelTrigger_dismiss() {
        // act
        cancelTrigger.onNext(())

        // assert
        XCTAssert(navigator.dismissCalled)
    }
}