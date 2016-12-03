#![allow(dead_code)]

use std::io::prelude::*;
use std::fs::File;
use std::collections::HashSet;

type Vec2 = (i32, i32);

#[derive(PartialEq, Debug)]
enum Turn {
  L,
  R,
}

impl Turn {
  fn parse(s: &str) -> Option<Turn> {
    match s.as_ref() {
      "L" => Some(Turn::L),
      "R" => Some(Turn::R),
      _ => None
    }
  }
}

#[derive(PartialEq, Debug)]
enum Direction {
  N,
  E,
  S,
  W,
}

impl Direction {
  fn to_vec(&self) -> Vec2 {
    match *self {
      Direction::N => (0, 1),
      Direction::E => (1, 0),
      Direction::S => (0, -1),
      Direction::W => (-1, 0),
    }
  }

  fn turn(self, t: Turn) -> Direction {
    match (self, t) {
      (Direction::N, Turn::L) => Direction::W,
      (Direction::E, Turn::L) => Direction::N,
      (Direction::S, Turn::L) => Direction::E,
      (Direction::W, Turn::L) => Direction::S,

      (Direction::N, Turn::R) => Direction::E,
      (Direction::E, Turn::R) => Direction::S,
      (Direction::S, Turn::R) => Direction::W,
      (Direction::W, Turn::R) => Direction::N,
    }
  }
}

#[derive(PartialEq, Debug)]
struct Instruction {
  turn: Turn,
  amount: i32,
}

impl Instruction {
  fn parse(s: &str) -> Instruction {
    let s = s.to_string();
    let (turn_string, amount_string) = s.split_at(1);
    let turn = Turn::parse(turn_string).expect(
      &format!("Unrecognized turn: {}", turn_string));
    let amount = amount_string.parse::<i32>().expect(
      &format!("Expected number, got: {}", amount_string));
    Instruction {
      turn: turn,
      amount: amount,
    }
  }
}

fn vec_add(v1: Vec2, v2: Vec2) -> Vec2 {
  match (v1, v2) {
    ((x1, y1), (x2, y2)) => (x1 + x2, y1 + y2),
  }
}

fn vec_scale(v: Vec2, s: i32) -> Vec2 {
  match v {
    (x, y) => (x * s, y * s),
  }
}

fn taxi_distance(v1: Vec2, v2: Vec2) -> i32 {
  match (v1, v2) {
    ((x1, y1), (x2, y2)) => (x1 - x2).abs() + (y1 - y2).abs(),
  }
}

fn main() {
  let mut f = File::open("input.txt").unwrap();
  let mut s = String::new();
  f.read_to_string(&mut s).unwrap();

  let instrs = s.split(",")
    .map(|x| Instruction::parse(x.trim()))
    .collect::<Vec<Instruction>>();

  let mut pos = (0, 0);
  let mut dir = Direction::N;

  let mut visited = HashSet::new();
  let mut answer: Option<Vec2> = None;

  for i in instrs {
    dir = dir.turn(i.turn);
    let dir_vec = dir.to_vec();
    for _ in 0..(i.amount) {
      pos = vec_add(pos, dir_vec);
      if visited.contains(&pos) && answer.is_none() {
        answer = Some(pos);
      } else {
        visited.insert(pos);
      }
    }
  }

  println!("Final position: {:?}", pos);
  println!("Location that was visited twice: {:?}", answer.unwrap());
  println!("Distance: {:?}", taxi_distance((0, 0), answer.unwrap()));
}

