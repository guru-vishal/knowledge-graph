INSERT INTO notes (id, title, content)
VALUES
    (1, 'Learning Python',
     'Learning Python fundamentals and programming.'),
    (2, 'Data Structures',
     'Studying arrays, trees, graphs, and algorithms.'),
    (3, 'Project Planning',
     'Organizing tasks and improving productivity.');

INSERT INTO tags (id, name)
VALUES
    (1, 'programming'),
    (2, 'learning'),
    (3, 'productivity');

INSERT INTO note_tags (note_id, tag_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (3, 3);

INSERT INTO links (source_id, target_id)
VALUES
    (1, 2),
    (3, 1);