export interface QA {
  question: string;
  answer: Answer;
}

export interface Answer {
    answer: string,
    timestamp: number,
    source: string,
    domain: string
}

export interface Service {
    name: string,
    service: string
}

export interface Settings {
    services: Service[]
}

export interface Health {
    status: string
}