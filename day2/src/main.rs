#![allow(dead_code)]

use std::io::prelude::*;
use std::fs::File;
use std::io::BufReader;

type Vec2 = (i32, i32);

#[derive(PartialEq, Debug)]
enum Direction {
  U,
  R,
  L,
  D,
}

impl Direction {
  fn to_vec(&self) -> Vec2 {
    match *self {
      Direction::U => (0, -1),
      Direction::R => (1, 0),
      Direction::L => (-1, 0),
      Direction::D => (0, 1),
    }
  }

  fn parse(s: &str) -> Direction {
    match s.as_ref() {
      "U" => Direction::U,
      "R" => Direction::R,
      "L" => Direction::L,
      "D" => Direction::D,
      _ => panic!("Unrecognized direction: {}", s),
    }
  }
}

fn vec_add(v1: Vec2, v2: Vec2) -> Vec2 {
  match (v1, v2) {
    ((x1, y1), (x2, y2)) => (x1 + x2, y1 + y2),
  }
}

/*
fn vec_clamp(v: Vec2, min: Vec2, max: Vec2) -> Vec2 {
  match (v, min, max) {
    ((x, y), (min_x, min_y), (max_x, max_y)) => {
      (
        if x < min_x { min_x } else if x > max_x { max_x } else { x },
        if y < min_y { min_y } else if y > max_y { max_y } else { y }
      )
    },
  }
}
*/

fn pos_to_key(pos: Vec2) -> Option<String> {
  //fukit
  (match pos {
    (2, 0) => Some("1"),

    (1, 1) => Some("2"),
    (2, 1) => Some("3"),
    (3, 1) => Some("4"),

    (0, 2) => Some("5"),
    (1, 2) => Some("6"),
    (2, 2) => Some("7"),
    (3, 2) => Some("8"),
    (4, 2) => Some("9"),

    (1, 3) => Some("A"),
    (2, 3) => Some("B"),
    (3, 3) => Some("C"),

    (2, 4) => Some("D"),

    _ => None,
  }).map(|s| s.to_string())
}

fn main() {
  let f = File::open("input.txt").unwrap();
  let file = BufReader::new(&f);
  //     1
  //   2 3 4
  // 5 6 7 8 9
  //   A B C
  //     D
  let mut pos = (0, 2);
  let mut code = String::from("");
  for line in file.lines() {
    let l = line.unwrap();
    let dirs = l.chars()
      .map(|c| Direction::parse(&c.to_string()))
      .collect::<Vec<Direction>>();
    for dir in dirs {
      let potential_new_pos = vec_add(pos, dir.to_vec());
      let is_legal = pos_to_key(potential_new_pos).is_some();
      if is_legal {
        pos = potential_new_pos;
      }
    }
    code.push_str(&pos_to_key(pos).unwrap());
  }
  println!("{}", code);
}

