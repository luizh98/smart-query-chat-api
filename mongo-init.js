db = db.getSiblingDB('meu_banco');

db.professor.insertMany([
  { _id: 1, nome: "João Silva", especialidade: "Matemática", descricao: "Ensino médio e vestibular" },
  { _id: 2, nome: "Maria Oliveira", especialidade: "Física", descricao: "Universitária, especialista em mecânica" },
  { _id: 3, nome: "Carlos Souza", especialidade: "Química", descricao: "Aulas práticas e teóricas" },
  { _id: 4, nome: "Ana Martins", especialidade: "Biologia", descricao: "Genética e evolução" },
  { _id: 5, nome: "Ricardo Lima", especialidade: "História", descricao: "História do Brasil e Geral" },
  { _id: 6, nome: "Fernanda Alves", especialidade: "Geografia", descricao: "Geopolítica e cartografia" },
  { _id: 7, nome: "Bruno Rocha", especialidade: "Inglês", descricao: "Conversação e exames internacionais" },
  { _id: 8, nome: "Patrícia Gomes", especialidade: "Literatura", descricao: "Literatura brasileira e mundial" },
  { _id: 9, nome: "Gabriel Mendes", especialidade: "Filosofia", descricao: "Ética e epistemologia" },
  { _id: 10, nome: "Juliana Costa", especialidade: "Sociologia", descricao: "Sociedade contemporânea" }
]);

db.aula.insertMany([
  { _id: 1, titulo: "Introdução à Álgebra", descricao: "Conceitos básicos para iniciantes" },
  { _id: 2, titulo: "Geometria Analítica", descricao: "Planos e retas no espaço" },
  { _id: 3, titulo: "Mecânica Clássica", descricao: "Movimento e forças" },
  { _id: 4, titulo: "Química Orgânica", descricao: "Cadeias carbônicas e funções" },
  { _id: 5,titulo: "Estequiometria", descricao: "Cálculos químicos fundamentais" },
  { _id: 6,titulo: "Biologia Celular", descricao: "Organelas e funções celulares" },
  { _id: 7,titulo: "Brasil Colônia", descricao: "Do descobrimento à independência" },
  { _id: 8,titulo: "Geopolítica Mundial", descricao: "Relações internacionais e conflitos" },
  { _id: 9, titulo: "Conversação Avançada em Inglês", descricao: "Prática intensiva" },
  { _id: 10, titulo: "Modernismo Brasileiro", descricao: "Semana de Arte Moderna e além" }
]);

db.agenda_professor.insertMany([
  { professor_id: 1, aula_id: 1, data_hora: ISODate("2025-07-15T14:00:00Z"), rocket: 5 },
  { professor_id: 1, aula_id: 2, data_hora: ISODate("2025-07-16T10:00:00Z"), rocket: 3 },
  { professor_id: 2, aula_id: 3, data_hora: ISODate("2025-07-15T09:00:00Z"), rocket: 4.2 },
  { professor_id: 3, aula_id: 4, data_hora: ISODate("2025-07-18T11:30:00Z"), rocket: 5  },
  { professor_id: 4, aula_id: 5, data_hora: ISODate("2025-07-15T15:45:00Z"), rocket: 3.9 },
  { professor_id: 5, aula_id: 6, data_hora: ISODate("2025-07-20T08:15:00Z"), rocket: 4.5 },
  { professor_id: 6, aula_id: 7, data_hora: ISODate("2025-07-21T13:20:00Z"), rocket: 4.3 },
  { professor_id: 7, aula_id: 8, data_hora: ISODate("2025-07-22T16:00:00Z"), rocket: 4.2 },
  { professor_id: 8, aula_id: 1, data_hora: ISODate("2025-07-23T10:40:00Z"), rocket: 4.1 },
  { professor_id: 9, aula_id: 10, data_hora: ISODate("2025-07-24T14:55:00Z"), rocket: 4 },
  { professor_id: 10, aula_id: 9, data_hora: ISODate("2025-07-25T09:05:00Z"), rocket: 5 }
]);