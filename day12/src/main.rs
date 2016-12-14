#![allow(dead_code)]

extern crate regex;
#[macro_use]
extern crate lazy_static;

use std::io::prelude::*;
use std::fs::File;
use std::io::BufReader;
use regex::Regex;
use std::error::Error;
use std::collections::HashMap;

lazy_static! {
  static ref ALPHA_RE: Regex = Regex::new(r"[a-zA-Z]+").unwrap();
  static ref NUM_RE: Regex = Regex::new(r"[0-9]+").unwrap();
}

#[derive(PartialEq, Clone, Debug)]
enum Src {
  Register(String),
  Value(i32),
}

#[derive(PartialEq, Clone, Debug)]
enum Instruction {
  Cpy(Src, String),
  Inc(String),
  Dec(String),
  Jnz(Src, i32),
}

use self::Instruction::*;

fn parse_src(s: &str) -> Result<Src, String> {
  if ALPHA_RE.is_match(s) {
    Ok(Src::Register(s.to_string()))
  } else if NUM_RE.is_match(s) {
    let n: i32 = try!(
      s.parse::<i32>().map_err(|e| e.description().to_string())
    );
    Ok(Src::Value(n))
  } else {
    Err("Invalid src".to_string())
  }
}

impl Instruction {
  fn from_string(s: &str) -> Result<Instruction, String> {
    let parts = s.split_whitespace().collect::<Vec<&str>>();
    let instr_type = try!(parts.first().ok_or("Missing instruction"));
    match *instr_type {
      "cpy" => {
        let arg1 = try!(parts.get(1).ok_or("Missing src".to_string()));
        let arg2 = try!(parts.get(2).ok_or("Missing dest".to_string()));
        let src = try!(parse_src(arg1));
        Ok(Cpy(src, arg2.to_string()))
      },
      "inc" | "dec" => {
        let arg1 = try!(parts.get(1).ok_or("Missing register".to_string()));
        Ok(if *instr_type == "inc" {
          Inc(arg1.to_string())
        } else {
          Dec(arg1.to_string())
        })
      },
      "jnz" => {
        let arg1 = try!(parts.get(1).ok_or("Missing src".to_string()));
        let arg2 = try!(parts.get(2).ok_or("Missing amount".to_string()));
        let src = try!(parse_src(arg1));
        let amount = try!(arg2.parse::<i32>().map_err(|e| e.description().to_string()));
        Ok(Jnz(src, amount))
      },
      _ => Err(format!("Unknown instruction type: {}", instr_type)),
    }
  }
}

fn main() {
  let f = File::open("input.txt").unwrap();
  let file = BufReader::new(&f);
  let instrs = file.lines()
    .map(|l| Instruction::from_string(&l.unwrap()).unwrap())
    .collect::<Vec<Instruction>>();
  let mut registers: HashMap<String, i32> = HashMap::new();
  let mut instr_pointer: i32 = 0;
  loop {
    match *instrs.get(instr_pointer as usize).unwrap() {
      Cpy(ref src, ref dest) => {
        match *src {
          Src::Register(ref name) => {
            let value_from_source_register = registers.get(name.as_str()).map(|x| *x).unwrap_or(0);
            registers.insert(dest.to_string(), value_from_source_register);
          },
          Src::Value(ref value) => {
            registers.insert(dest.to_string(), *value);
          },
        }
      },
      Inc(ref reg) => {
        let cur_value: i32 = registers.get(reg.as_str()).map(|x| *x).unwrap_or(0);
        registers.insert(reg.to_string(), cur_value + 1);
      },
      Dec(ref reg) => {
        let cur_value: i32 = registers.get(reg.as_str()).map(|x| *x).unwrap_or(0);
        registers.insert(reg.to_string(), cur_value - 1);
      },
      Jnz(ref src, ref amount) => {
        let value = match *src {
          Src::Register(ref name) => registers.get(name.as_str()).map(|x| *x).unwrap_or(0),
          Src::Value(ref value) => *value,
        };
        if value != 0 {
          instr_pointer = instr_pointer + amount - 1; // Since we increment below.
        }
      },
    }
    instr_pointer += 1;
    if instr_pointer >= (instrs.len() as i32) {
      break;
    }
  }
  println!("{:?}", registers);
}

