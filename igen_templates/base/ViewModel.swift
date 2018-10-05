struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModelType {
    struct Input {

    }

    struct Output {

    }

    func transform(_ input: Input) -> Output {
        return Output()
    }
}
